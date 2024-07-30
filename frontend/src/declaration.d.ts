declare module "*.png" {
    const value: string
    export default value
}

declare module "@heroicons/vue/*" {
    import { DefineComponent } from "vue"
    const component: DefineComponent<{}, {}, any>
    export default component
}

declare module "@heroicons/vue/24/outline/EnvelopeIcon" {
    import { DefineComponent } from "vue"
    const component: DefineComponent<{}, {}, any>
    export default component
}
