export interface UserJobResponse {
    job: {
        id: number;
        created_at: string;
        linkedin_url: string;
        company_name: string;
        job_title: string;
        last_update: string;
        company_url?: string;
        date_posted?: string;
        location_city?: string;
        location_country?: string;
        ai_summary?: string;
        job_metadata?: any;
        linkedin_job_id?: string;
    };
    status: string;
    contacts?: Contact[];
}

export interface Contact {
    id: number;
    linkedin_id?: string;
    name: string;
    title: string;
    email: string;
    linkedin_url?: string;
}

export type JobStatus = 'Applied' | 'Not Applied' | 'Interviewing' | 'Rejected' | 'Offer';

export interface Job {
    id: string;
    company: string;
    name: string;
    datePosted: string;
    location: string;
    keyContacts: Contact[];
    status: JobStatus;
    selected: boolean;
}

export interface AISummary {
    id: string;
    skills: string[];
    personalizations: string[];
    connections: string[];
}

export interface Filter {
    column: keyof Job;
    condition: 'contains' | 'equals' | 'startsWith' | 'endsWith';
    value: string;
}

export interface SortConfig {
    column: keyof Job | null;
    direction: 'asc' | 'desc';
}