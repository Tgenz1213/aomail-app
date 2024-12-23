import { i18n, timezoneSelected } from "./preferences";

export function formatInteger(count: number): string {
    if (isNaN(count) || count === null) {
        return "N/A";
    }

    if (count >= 1_000_000_000) {
        return `${(count / 1_000_000_000).toFixed(1)}B`;
    } else if (count >= 1_000_000) {
        return `${(count / 1_000_000).toFixed(1)}M`;
    } else if (count >= 1_000) {
        return count.toLocaleString();
    } else {
        return count.toString();
    }
}

export function formatFloat(value: number): string {
    if (isNaN(value) || value === null) {
        return "N/A";
    }

    if (value >= 1_000_000_000) {
        return `${(value / 1_000_000_000).toFixed(2)}B`;
    } else if (value >= 1_000_000) {
        return `${(value / 1_000_000).toFixed(2)}M`;
    } else if (value >= 1_000) {
        return `${(value / 1_000).toFixed(2)}K`;
    } else {
        return value.toFixed(2);
    }
}

export const formatSentDateAndTime = (sentDateString: string, sentTimeString: string) => {
    const sentDateAndTimeString = `${sentDateString}T${sentTimeString}:00Z`;
    const sentDateObject = new Date(sentDateAndTimeString);

    const formattedSentDateAndTime = sentDateObject.toLocaleString(i18n.global.locale, {
        timeZone: timezoneSelected.value,
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });

    return formattedSentDateAndTime;
};

export const formatSentDate = (sentDateString: string) => {
    const sentDateObject = new Date(`${sentDateString}T00:00:00Z`);

    const formattedSentDate = sentDateObject.toLocaleDateString(i18n.global.locale, {
        timeZone: timezoneSelected.value,
        year: "numeric",
        month: "long",
        day: "numeric",
        weekday: "long",
    });

    return formattedSentDate;
};

export const formatSentTime = (sentDateString: string, sentTimeString: string) => {
    const sentDateTimeString = `${sentDateString}T${sentTimeString}:00Z`;
    const sentDateTimeObject = new Date(sentDateTimeString);

    const formattedSentTime = sentDateTimeObject.toLocaleTimeString(i18n.global.locale, {
        timeZone: timezoneSelected.value,
        hour: "2-digit",
        minute: "2-digit",
    });

    return formattedSentTime;
};
