import { UserJobResponse, Job, JobStatus, Filter, SortConfig, Contact } from "@/utils/types"
import { aiSummaries } from "./constants";

export function transformJobResponse(userJob: UserJobResponse): Job {
    console.log(userJob.contacts)
    return {
        id: userJob.job.id.toString(),
        company: userJob.job.company_name,
        name: userJob.job.job_title,
        datePosted: userJob.job.date_posted || userJob.job.created_at.split('T')[0],
        location: userJob.job.location_city && userJob.job.location_country
            ? `${userJob.job.location_city}, ${userJob.job.location_country}`
            : 'Unknown',
        keyContacts: userJob.contacts || [],
        status: userJob.status as JobStatus,
        selected: false,
    };
}


export const applyFiltersAndSort = (
    jobPostings: Job[],
    filters: Filter[],
    sortConfig: SortConfig
): Job[] => {
    let result = [...jobPostings]
    filters.forEach(filter => {
        result = result.filter(job => {
            const value = job[filter.column]
            if (typeof value === 'string') {
                switch (filter.condition) {
                    case 'contains':
                        return value.toLowerCase().includes(filter.value.toLowerCase())
                    case 'equals':
                        return value.toLowerCase() === filter.value.toLowerCase()
                    case 'startsWith':
                        return value.toLowerCase().startsWith(filter.value.toLowerCase())
                    case 'endsWith':
                        return value.toLowerCase().endsWith(filter.value.toLowerCase())
                }
            }
            return true
        })
    })

    if (sortConfig.column) {
        result.sort((a, b) => {
            if (a[sortConfig.column!] < b[sortConfig.column!]) {
                return sortConfig.direction === 'asc' ? -1 : 1
            }
            if (a[sortConfig.column!] > b[sortConfig.column!]) {
                return sortConfig.direction === 'asc' ? 1 : -1
            }
            return 0
        })
    }

    return result
}

// This is a placeholder
export const generateEmailCopy = (contact: Contact, job: Job) => {
    const summary = aiSummaries.find(s => s.id === job.id)
    return `Dear ${contact.name},

I hope this email finds you well. I'm reaching out regarding the ${job.name} position at ${job.company}. As a passionate professional in this field, I'm excited about the opportunity to contribute to your team.

${summary?.personalizations[0]}

My background includes expertise in ${summary?.skills.join(", ")}, which I believe aligns well with the requirements of this role. ${summary?.connections[0]}

I've attached my resume for your review. I would welcome the opportunity to discuss how my skills and experience could benefit ${job.company}.

Thank you for your time and consideration.

Best regards,
[Your Name]`
}