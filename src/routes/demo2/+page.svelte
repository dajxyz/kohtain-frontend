<script lang='ts'>
  import Calendar from "lucide-svelte/icons/calendar";
  import House from "lucide-svelte/icons/house";
  import Inbox from "lucide-svelte/icons/inbox";
  import Search from "lucide-svelte/icons/search";
  import Settings from "lucide-svelte/icons/settings";
import * as Sidebar from "$lib/components/ui/sidebar/index.js";
// Menu items.
const items = [
    {
      title: "Home",
      url: "#",
      icon: House,
    },
    {
      title: "Inbox",
      url: "#",
      icon: Inbox,
    },
    {
      title: "Calendar",
      url: "#",
      icon: Calendar,
    },
    {
      title: "Search",
      url: "#",
      icon: Search,
    },
    {
      title: "Settings",
      url: "#",
      icon: Settings,
    },
  ];



export let data

let utteranceBlocks = data.trnscript.diarization_enhanced.results
// console.log(typeof(utteranceBlocks))

let värit = [
	"#78e9ff55",
	"#b3000055",
	"#00ffd255",
	"#e3008755",
	"#00720055",
	"#ff6fff55",
	"#c6bb0055",
	"#22006d55",
	"#95a72955",
	"#a871ff55",
	"#00a97355",
	"#ff79ff55",
	"#64a15555",
	"#db63db55",
	"#00360755",
	"#ff7be555",
	"#002e0055",
	"#c30b4f55",
	"#00ecff55",
	"#bc2f0055",
	"#8ef8ff55",
	"#bc0a2b55",
	"#00b4c555",
	"#ff783955",
	"#00409fff",
	"#726600ff",
	"#003381ff",
	"#ffebc0ff",
	"#003f78ff",
	"#efd5a6ff",
	"#764ea1ff",
	"#711800ff",
	"#00acc4ff",
	"#50121aff",
	"#00a0bdff",
	"#ff9296ff",
	"#001d1aff",
	"#00769aff",
	"#006256ff",
	"#005471ff"
]

</script>

<Sidebar.Root>
	<Sidebar.Content>
	  <Sidebar.Group>
		<Sidebar.GroupLabel>Application</Sidebar.GroupLabel>
		<Sidebar.GroupContent>
		  <Sidebar.Menu>
			{#each items as item (item.title)}
			  <Sidebar.MenuItem>
				<Sidebar.MenuButton>
				  {#snippet child({ props })}
					<a href={item.url} {...props}>
					  <item.icon />
					  <span>{item.title}</span>
					</a>
				  {/snippet}
				</Sidebar.MenuButton>
			  </Sidebar.MenuItem>
			{/each}
		  </Sidebar.Menu>
		</Sidebar.GroupContent>
	  </Sidebar.Group>
	</Sidebar.Content>
  </Sidebar.Root>
  
