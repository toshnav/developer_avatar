import httpx
from typing import List, Dict, Any, Optional

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def get_activity(self, username: str, date: str) -> List[Dict[str, Any]]:
        """
        Fetches GitHub activity for a user across all repositories on a specific date.
        """
        if not self.token:
            return [{"error": "GitHub token not configured"}]

        activity_list = []
        async with httpx.AsyncClient() as client:
            try:
                # 1. Identify active repositories from User Events
                events_url = f"https://api.github.com/users/{username}/events"
                params = {"per_page": 100}
                
                active_repos = set()
                page = 1
                
                # Scan events to find active repos and non-commit events
                while True:
                    response = await client.get(events_url, headers=self.headers, params={**params, "page": page})
                    if response.status_code != 200:
                        break
                        
                    events = response.json()
                    
                    if not events:
                        break
                    
                    for event in events:
                        created_at = event.get("created_at", "")[:10] # YYYY-MM-DD
                        
                        if created_at == date:
                            repo_name = event.get("repo", {}).get("name")
                            event_type = event.get("type")
                            
                            if event_type == "PushEvent":
                                if repo_name:
                                    active_repos.add(repo_name)
                            elif event_type == "CreateEvent":
                                if repo_name:
                                    active_repos.add(repo_name)
                                # Log creation event
                                ref_type = event.get("payload", {}).get("ref_type")
                                ref = event.get("payload", {}).get("ref", "unknown")
                                activity_list.append({
                                    "type": event_type,
                                    "repo": repo_name,
                                    "ref": ref,
                                    "ref_type": ref_type,
                                    "summary": f"Created {ref_type} '{ref}'",
                                    "key": f"create-{ref}-{created_at}",
                                    "description": f"Created {ref_type} '{ref}' in {repo_name}"
                                })
                            elif event_type == "PullRequestEvent":
                                repo_name = event.get("repo", {}).get("name", "unknown")
                                action = event.get("payload", {}).get("action")
                                title = event.get("payload", {}).get("pull_request", {}).get("title")
                                pr_url = event.get("payload", {}).get("pull_request", {}).get("html_url")
                                activity_list.append({
                                    "type": event_type,
                                    "repo": repo_name,
                                    "action": action,
                                    "summary": f"PR {action}: {title}",
                                    "key": pr_url,
                                    "description": f"Pull Request: {title} ({action})"
                                })
                                
                        elif created_at < date:
                            # Events are sorted by date
                            break
                    else:
                        # Continue to next page
                        page += 1
                        if page > 3: break
                        continue
                    break # Break out of while loop if we hit older dates

                # 2. Fetch specific commits for active repositories
                for repo in active_repos:
                    try:
                        commits_url = f"https://api.github.com/repos/{repo}/commits"
                        commit_params = {
                            "author": username,
                            "since": f"{date}T00:00:00Z",
                            "until": f"{date}T23:59:59Z",
                            "per_page": 100
                        }
                        
                        resp = await client.get(commits_url, headers=self.headers, params=commit_params)
                        if resp.status_code == 200:
                            commits = resp.json()
                            
                            for commit in commits:
                                msg = commit.get("commit", {}).get("message", "")
                                sha = commit.get("sha", "")
                                summary = msg.split('\n')[0]
                                activity_list.append({
                                    "type": "Commit",
                                    "repo": repo,
                                    "key": sha,
                                    "summary": summary,
                                    "description": msg
                                })
                    except Exception:
                        continue # Skip repo on error

                return activity_list
            except Exception as e:
                return [{"error": f"Error fetching GitHub data: {str(e)}"}]
