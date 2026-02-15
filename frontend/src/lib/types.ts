export interface DailyActivityRequest {
    developer_email: string;
    date: string;
}

export interface IssueDetail {
    key: string;
    summary: string;
    status: string;
    time_spent: number;
    comments: string[];
}

export interface ActivitySummary {
    total_hours: number;
    issues_worked_on: string[];
    details: IssueDetail[];
    summary: string;
    status: string;
}
