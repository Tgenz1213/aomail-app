<template>
    <nav>
        <ol role="list" class="flex items-center" v-if="step === 0">
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                    aria-current="step"
                >
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="goStepPreferences"
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="goStep2"
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
            <li class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 1">
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="goStep0"
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                    aria-current="step"
                >
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="goStepCategories"
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
            <li class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 2">
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="goStep0"
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="goStep1"
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                    aria-current="step"
                >
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    @click="submitSignupData"
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
            <li class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 3">
            <li class="relative pr-2 sm:pr-4">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                    aria-current="step"
                >
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                </a>
            </li>
            <li class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                >
                    <span
                        class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                        aria-hidden="true"
                    ></span>
                </a>
            </li>
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 4">
            <li class="relative pr-2 sm:pr-4">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                >
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative pr-6 sm:pr-16">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path
                            fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </a>
            </li>
            <li class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-gray-500"></div>
                </div>
                <a
                    class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                    aria-current="step"
                >
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                </a>
            </li>
        </ol>
    </nav>
</template>

<script setup lang="ts">
import { inject, ref, Ref } from "vue";


const props = defineProps<{
    signUpPage: string; // todo: by default its equals to "signUp" => there are only two possibilities with "signUpLink"
}>();


if (props.signUpPage == "signUp") {
    goStep0
    goStep1
}

const step = inject<Ref<number>>("step") || ref(0);
</script>
