import { API_BASE_URL, MICROSOFT } from "./const"
import { fetchWithToken } from "./security"
import { i18n } from "../pages/Settings/utils/preferences"

interface Person {
    email: string
}

interface SendEmailResult {
    type: "error" | "success"
    title: string
    message: string
}

export async function sendEmail(
    emailSubject: string,
    emailBody: string,
    selectedPeople: { value: Person[] },
    selectedCc: { value: Person[] },
    selectedCci: { value: Person[] },
    emailSelected: { value: string },
    fileObjects: { value: File[] }
): Promise<SendEmailResult> {
    if (!emailSubject.trim()) {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject"),
        }
    } else if (emailBody === "<p><br></p>") {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoObject"),
        }
    } else if (selectedPeople.value.length === 0) {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient"),
        }
    }

    const formData = new FormData()

    formData.append("subject", emailSubject)
    formData.append("message", emailBody)
    fileObjects.value.forEach((file) => formData.append("attachments", file))

    selectedPeople.value.forEach((person) => formData.append("to", person.email))
    if (selectedCc.value.length > 0) {
        selectedCc.value.forEach((person) => formData.append("cc", person.email))
    }
    if (selectedCci.value.length > 0) {
        selectedCci.value.forEach((person) => formData.append("cci", person.email))
    }
    formData.append("email", emailSelected.value)

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/social_api/send_email/`, {
            method: "POST",
            body: formData,
        })

        if (!response) {
            return {
                type: "error",
                title: "No response from server",
                message: "Verify your internet connection",
            }
        }

        if (response.status === 200) {
            localStorage.removeItem("uploadedFiles")

            return {
                type: "success",
                title: i18n.global.t("constants.popUpConstants.successMessages.success"),
                message: i18n.global.t("constants.popUpConstants.successMessages.emailSuccessfullySent"),
            }
        } else {
            return {
                type: "error",
                title: "Error in response",
                message: `HTTP error! status: ${response.status}`,
            }
        }
    } catch (error: unknown) {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: (error as Error).message,
        }
    }
}

export async function scheduleSendEmail(
    emailSubject: string,
    emailBody: string,
    selectedPeople: { value: Person[] },
    selectedCc: { value: Person[] },
    selectedCci: { value: Person[] },
    emailSelected: { value: string },
    fileObjects: { value: File[] },
    emailsLinked: { value: { email: string; typeApi: string }[] },
    scheduleDate: string
): Promise<SendEmailResult> {
    for (const tupleEmail of emailsLinked.value) {
        if (emailSelected.value === tupleEmail.email && tupleEmail.typeApi !== MICROSOFT) {
            return {
                type: "error",
                title: "Email service provider not supported",
                message: "Scheduled send is only available for Outlook accounts",
            }
        }
    }

    if (!emailSubject.trim()) {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject"),
        }
    } else if (emailBody === "<p><br></p>") {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoObject"),
        }
    } else if (selectedPeople.value.length === 0) {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient"),
        }
    }

    const formData = new FormData()

    formData.append("subject", emailSubject)
    formData.append("message", emailBody)
    fileObjects.value.forEach((file) => formData.append("attachments", file))

    selectedPeople.value.forEach((person) => formData.append("to", person.email))
    if (selectedCc.value.length > 0) {
        selectedCc.value.forEach((person) => formData.append("cc", person.email))
    }
    if (selectedCci.value.length > 0) {
        selectedCci.value.forEach((person) => formData.append("cci", person.email))
    }
    formData.append("email", emailSelected.value)
    formData.append("datetime", scheduleDate)

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/social_api/send_schedule_email/`, {
            method: "POST",
            body: formData,
        })

        if (!response) {
            return {
                type: "error",
                title: "No response from server",
                message: "Verify your internet connection",
            }
        }

        if (response.status === 200) {
            localStorage.removeItem("uploadedFiles")

            return {
                type: "success",
                title: "Email scheduled successfully!",
                message: "Your email will be sent on time",
            }
        } else {
            return {
                type: "error",
                title: "Error in response",
                message: `HTTP error! status: ${response.status}`,
            }
        }
    } catch (error: unknown) {
        return {
            type: "error",
            title: i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            message: (error as Error).message,
        }
    }
}
