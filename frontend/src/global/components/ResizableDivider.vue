<template>
    <div class="w-1 bg-gray-200 cursor-col-resize h-full" @mousedown="startResize"></div>
</template>

<script setup lang="ts">
const props = defineProps<{
    onResize: (widthPercentage: number) => void;
}>();

const startResize = (e: MouseEvent) => {
    e.preventDefault();

    const handleMouseMove = (e: MouseEvent) => {
        const windowWidth = window.innerWidth - 90; // Subtract navbar width
        const mouseX = e.clientX - 90; // Subtract navbar offset
        const percentage = (mouseX / windowWidth) * 100;

        if (percentage >= 30 && percentage <= 70) {
            props.onResize(percentage);
        }
    };

    const stopResize = () => {
        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", stopResize);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", stopResize);
};
</script>
