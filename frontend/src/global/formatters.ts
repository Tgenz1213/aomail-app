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
