<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
   
    let { children } = $props();
  </script>
   
   <Sidebar.Provider style="--sidebar-width: 350px;">
    <AppSidebar />
    <main>
      {@render children?.()}
    </main>
  </Sidebar.Provider>