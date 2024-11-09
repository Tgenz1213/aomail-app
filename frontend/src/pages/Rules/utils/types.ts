export interface RuleData {
    id: number;
    priority?: string;
    categoryId?: number;
    category?: string;
    username?: string;
    email: string;
    block?: boolean;
    infoAI?: string;
}

export interface FilterPayload {
    advanced?: boolean;
    search?: string;
    sort?: string;
    order?: string;
    block?: boolean;
    categoryName?: string;
    priority?: string;
    senderName?: string;
    senderEmail?: string;
}
