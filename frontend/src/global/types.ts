import { Component as VueComponent } from "vue";
import {
    ANSWER_REQUIRED,
    GOOGLE,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    MICROSOFT,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    USELESS,
} from "./const";

export type EmailProvider = typeof GOOGLE | typeof MICROSOFT;

export interface KeyValuePair {
    key: string;
    value: string;
}

export interface AttachmentType {
    extension: string;
    name: string;
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
    target?: string;
}

interface Sender {
    email: string;
    name: string;
}

interface EmailRule {
    hasRule: boolean;
    ruleId: number;
}

interface EmailAttachment {
    attachmentName: string;
    attachmentId: number;
}

interface EmailFlags {
    spam: boolean;
    scam: boolean;
    newsletter: boolean;
    notification: boolean;
    meeting: boolean;
}

export interface FetchDataResult {
    success: boolean;
    data?: any;
    blob?: any;
    error?: string;
}

export interface Recipient {
    username?: string;
    email: string;
}

export interface Email {
    id?: number;
    subject: string;
    sender: Sender;
    providerId: string;
    shortSummary?: string;
    oneLineSummary?: string;
    cc: Sender[];
    bcc: Sender[];
    read?: boolean;
    answerLater?: boolean;
    rule?: EmailRule;
    hasAttachments: boolean;
    attachments: EmailAttachment[];
    sentDate: string;
    sentTime: string;
    answer?: boolean;
    archive?: boolean;
    relevance?: string;
    priority?: string;
    flags?: EmailFlags;
    category?: string;
    htmlContent?: string;
}

export interface EmailDetails {
    data: {
        [category: string]: {
            [priority: string]: Email[];
        };
    };
}

export interface EmailLinked {
    email: string;
    typeApi: string;
}

export interface UploadedFile {
    name: string;
    size: number;
}

export interface AiRecipient {
    username: string;
    email: string | { username: string; email: string }[];
}

export interface Agent {
    id: string;
    agent_name: string;
    ai_template: string;
    email_example?: string;
    picture: string;
    length: string;
    formality: string;
    icon_name: string;
}

export interface Frequency {
    key: string;
    label: string;
    priceSuffix?: string;
}

export interface AomailSearchFilter {
    advanced?: boolean;
    emailProvider?: string[];
    subject?: string;
    senderEmail?: string;
    senderName?: string;
    CCEmails?: string[];
    CCNames?: string[];
    category?: string;
    emailAddresses?: string[];
    archive?: boolean;
    replyLater?: boolean;
    read?: boolean;
    sentDate?: Date;
    readDate?: Date;
    answer?: (typeof ANSWER_REQUIRED | typeof MIGHT_REQUIRE_ANSWER | typeof NO_ANSWER_REQUIRED)[];
    relevance?: (typeof HIGHLY_RELEVANT | typeof POSSIBLY_RELEVANT | typeof NOT_RELEVANT)[];
    priority?: (typeof IMPORTANT | typeof INFORMATIVE | typeof USELESS)[];
    hasAttachments?: boolean;
    spam?: boolean;
    scam?: boolean;
    newsletter?: boolean;
    notification?: boolean;
    meeting?: boolean;
}

export interface ApiSearchFilter {
    advanced?: boolean;
    emailProvider?: string[];
    fileExtensions?: string[];
    filenames?: string[];
    searchIn?: Record<string, boolean>;
    fromAddresses?: string[];
    toAddresses?: string[];
    subject?: string;
    body?: string;
    dateFrom?: string; // Format allowed: YYYY-MM-DD
}

export type Message = {
    textHtml: string;
    isUser: boolean;
    buttonOptions?: KeyValuePair[];
};

export interface Filter {
    id?: number;
    name: string;
    important: boolean;
    informative: boolean;
    useless: boolean;
    read: boolean;
    notification: boolean;
    newsletter: boolean;
    spam: boolean;
    scam: boolean;
    meeting: boolean;
    relevance?: string;
    answer?: string;
    category?: string;
}
