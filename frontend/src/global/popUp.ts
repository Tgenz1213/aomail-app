import { Ref } from "vue";
import { POP_UP_ERROR_COLOR, POP_UP_SUCCESS_COLOR } from "./const";

export function displayErrorPopup(
    showNotification: Ref<boolean>,
    notificationTitle: Ref<string>,
    notificationMessage: Ref<string>,
    backgroundColor: Ref<string>,
    title: string,
    message: string
) {
    backgroundColor.value = POP_UP_ERROR_COLOR;
    notificationTitle.value = title;
    notificationMessage.value = message;
    showNotification.value = true;

    setTimeout(() => {
        showNotification.value = false;
    }, 4000);
}

export function displaySuccessPopup(
    showNotification: Ref<boolean>,
    notificationTitle: Ref<string>,
    notificationMessage: Ref<string>,
    backgroundColor: Ref<string>,
    title: string,
    message: string
) {
    backgroundColor.value = POP_UP_SUCCESS_COLOR;
    notificationTitle.value = title;
    notificationMessage.value = message;
    showNotification.value = true;

    setTimeout(() => {
        showNotification.value = false;
    }, 4000);
}
