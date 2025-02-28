<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    export const prerender = true;

    let { children } = $props();
  </script>
   
   <Sidebar.Provider style="--sidebar-width: 350px;">
    <AppSidebar />
    <main class="bg-[#D9D9D9]">
      {@render children?.()}
    </main>
  </Sidebar.Provider>

