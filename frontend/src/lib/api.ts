import { ActivitySummary } from './types';

const API_BASE_URL = 'http://localhost:8000';

export async function fetchActivitySummary(email: string, date: string, llmProvider: string = 'azure'): Promise<ActivitySummary> {
    const response = await fetch(`${API_BASE_URL}/activity/summary`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ developer_email: email, date, llm_provider: llmProvider }),
    });

    if (!response.ok) {
        throw new Error('Failed to fetch activity summary');
    }

    return response.json();
}
