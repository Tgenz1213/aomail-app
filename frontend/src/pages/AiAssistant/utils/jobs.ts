import { i18n } from "@/global/preferences";

interface Profile {
    title: string;
    description: string;
    keywords: string[];
    important: string;
    informative: string;
    useless: string;
}

export function getPredefinedProfiles(): Profile[] {
    return [
        {
            title: i18n.global.t("aiAssistantPage.jobs.softwareEngineer.title"),
            description: i18n.global.t("aiAssistantPage.jobs.softwareEngineer.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.softwareEngineer.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.softwareEngineer.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.softwareEngineer.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.softwareEngineer.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.itSupport.title"),
            description: i18n.global.t("aiAssistantPage.jobs.itSupport.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.itSupport.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.itSupport.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.itSupport.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.itSupport.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.teacher.title"),
            description: i18n.global.t("aiAssistantPage.jobs.teacher.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.teacher.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.teacher.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.teacher.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.teacher.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.student.title"),
            description: i18n.global.t("aiAssistantPage.jobs.student.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.student.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.student.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.student.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.student.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.nurse.title"),
            description: i18n.global.t("aiAssistantPage.jobs.nurse.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.nurse.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.nurse.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.nurse.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.nurse.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.manager.title"),
            description: i18n.global.t("aiAssistantPage.jobs.manager.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.manager.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.manager.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.manager.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.manager.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.salesRep.title"),
            description: i18n.global.t("aiAssistantPage.jobs.salesRep.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.salesRep.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.salesRep.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.salesRep.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.salesRep.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.lawyer.title"),
            description: i18n.global.t("aiAssistantPage.jobs.lawyer.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.lawyer.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.lawyer.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.lawyer.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.lawyer.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.creative.title"),
            description: i18n.global.t("aiAssistantPage.jobs.creative.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.creative.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.creative.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.creative.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.creative.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.restaurant.title"),
            description: i18n.global.t("aiAssistantPage.jobs.restaurant.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.restaurant.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.restaurant.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.restaurant.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.restaurant.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.beauty.title"),
            description: i18n.global.t("aiAssistantPage.jobs.beauty.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.beauty.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.beauty.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.beauty.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.beauty.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.smallBusiness.title"),
            description: i18n.global.t("aiAssistantPage.jobs.smallBusiness.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.smallBusiness.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.smallBusiness.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.smallBusiness.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.smallBusiness.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.freelance.title"),
            description: i18n.global.t("aiAssistantPage.jobs.freelance.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.freelance.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.freelance.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.freelance.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.freelance.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.fieldTech.title"),
            description: i18n.global.t("aiAssistantPage.jobs.fieldTech.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.fieldTech.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.fieldTech.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.fieldTech.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.fieldTech.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.researcher.title"),
            description: i18n.global.t("aiAssistantPage.jobs.researcher.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.researcher.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.researcher.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.researcher.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.researcher.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.construction.title"),
            description: i18n.global.t("aiAssistantPage.jobs.construction.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.construction.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.construction.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.construction.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.construction.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.driver.title"),
            description: i18n.global.t("aiAssistantPage.jobs.driver.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.driver.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.driver.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.driver.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.driver.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.admin.title"),
            description: i18n.global.t("aiAssistantPage.jobs.admin.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.admin.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.admin.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.admin.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.admin.useless"),
        },
        {
            title: i18n.global.t("aiAssistantPage.jobs.finance.title"),
            description: i18n.global.t("aiAssistantPage.jobs.finance.description"),
            keywords: i18n.global.tm("aiAssistantPage.jobs.finance.keywords"),
            important: i18n.global.t("aiAssistantPage.jobs.finance.important"),
            informative: i18n.global.t("aiAssistantPage.jobs.finance.informative"),
            useless: i18n.global.t("aiAssistantPage.jobs.finance.useless"),
        },
    ];
}
