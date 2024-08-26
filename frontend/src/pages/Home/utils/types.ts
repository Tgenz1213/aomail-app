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
  scam: boolean;
  meeting: boolean;
  relevance?: string | undefined;
  answer?: string | undefined; 
  category?: string;
}
