export interface DailyActivityRequest {
    developer_email: string;
    date: string;
}

export interface ActivitySummary {
    total_hours: number;
    issues_worked_on: string[];
    summary: string;
    status: string;
}
