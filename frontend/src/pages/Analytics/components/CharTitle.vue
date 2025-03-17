<template>
    <div class="relative w-full">
        <div class="absolute inset-0 flex items-center" aria-hidden="true">
            <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center">
            <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                <slot></slot>
            </span>
        </div>
    </div>
</template>
