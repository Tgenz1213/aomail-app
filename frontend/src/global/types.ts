import { Component as VueComponent } from "vue";

export interface KeyValuePair {
    key: string;
    value: string;
}

export interface EmailSender {
    id?: number;
    username: string;
    email: string;
}

export interface Category {
    name: string;
    description: string;
}

export interface NavigationPage {
    name: string;
    href: string;
    icon: VueComponent;
    current?: boolean;
}


export interface Email {
    id: string;
    subject: string;
    sender: {
        name: string;
        email: string;
    };
    sentDate: string;
    sentTime: string;
    priority: 'important' | 'informative' | 'useless';
    category: string;
    read: boolean;
    answer_later: boolean;
    oneLineSummary: string;
    shortSummary: string;
    html_content?: string;
    flags: {
        meeting: boolean;
        newsletter: boolean;
        notification: boolean;
        scam: boolean;
        spam: boolean;
    };
    hasAttachments: boolean;
    attachments?: Array<{
        attachmentId: string;
        attachmentName: string;
    }>;
    rule: {
        hasRule: boolean;
        ruleId?: string;
    };
}
