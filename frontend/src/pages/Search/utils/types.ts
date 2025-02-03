import { Email, EmailProvider } from "@/global/types";

export type EmailApiIds = {
    [key in EmailProvider]?: Record<string, string[]>; // string represents the email address
};

export type EmailApiListType = {
    [key in EmailProvider]?: Record<string, Email[]>;
};
