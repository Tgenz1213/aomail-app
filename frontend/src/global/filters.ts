import { postData } from "./fetchData";
import { Filter } from "./types";
import { i18n } from "@/global/preferences";

export async function createDefaultFilters(categoryName: string) {
    const ImportantEmailsFilter: Filter = {
        name: i18n.global.t("constants.ruleModalConstants.important"),
        important: true,
        informative: false,
        category: categoryName,
        useless: false,
        read: false,
        notification: true,
        newsletter: false,
        spam: false,
        scam: false,
        meeting: true,
    };

    const InformativeEmailsFilter: Filter = {
        name: i18n.global.t("constants.ruleModalConstants.informative"),
        important: false,
        informative: true,
        category: categoryName,
        useless: false,
        read: false,
        notification: true,
        newsletter: true,
        spam: false,
        scam: false,
        meeting: true,
    };

    await postData("create_filter/", ImportantEmailsFilter);
    await postData("create_filter/", InformativeEmailsFilter);
}
