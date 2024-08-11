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

export interface RuleData {
  id: string;
  username: string;
  email: string;
  category?: string;
  priority: string;
  mailStop: boolean;
}
