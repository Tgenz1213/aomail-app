export interface RuleData {
    id?: number;
    logicalOperator: "AND" | "OR";
    // --- email triggers --- //
    domains?: string[];
    senderEmails?: string[];
    hasAttachements?: boolean;
    // --- after AI processing triggers --- //
    categories?: string[];
    priorities?: string[];
    answers?: string[];
    relevances?: string[];
    flags?: string[];
    // --- AI triggers --- //
    emailDealWith?: string;

    // --- static actions --- //
    actionTransferRecipients?: string[];
    actionSetFlags?: string[];
    actionMarkAs?: string[];
    actionDelete?: boolean;
    actionSetCategory?: string;
    actionSetPriority?: string;
    actionSetRelevance?: string;
    actionSetAnswer?: string;
    // --- AI actions --- //
    actionReplyPrompt?: string;
    actionReplyRecipients?: string[];
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
