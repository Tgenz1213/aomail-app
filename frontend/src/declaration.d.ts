declare module "*.png" {
    const value: string;
    export default value;
}

declare module "@heroicons/vue/*" {
    import { DefineComponent } from "vue";
    const component: DefineComponent<object, object, any>;
    export default component;
}

declare module "@heroicons/vue/24/outline/*" {
    import { DefineComponent } from "vue";
    const component: DefineComponent<object, object, any>;
    export default component;
}

declare module "moment-timezone" {
    import moment from "moment";
    export = moment;
}

declare module "*.vue" {
    import { DefineComponent } from "vue";
    const component: DefineComponent<object, object, any>;
    export default component;
}

declare module "vue3-timepicker" {
    import { Component } from "vue";
    const TimePicker: Component;
    export default TimePicker;
}

declare module "vue-flag-icon";
