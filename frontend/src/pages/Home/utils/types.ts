export interface Tab {
  id: string;
  name: string;
}

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
  scams: boolean;
  meeting: boolean;
  relevance?: '' | 'high' | 'medium' | 'low';
  answer: string;
  category?: string;
}
