<script lang="ts" module>
	import ArchiveX from 'lucide-svelte/icons/archive-x';
	import File from 'lucide-svelte/icons/file';
	import Inbox from 'lucide-svelte/icons/inbox';
	import Send from 'lucide-svelte/icons/send';
	import Trash2 from 'lucide-svelte/icons/trash-2';
	import AddFile from 'lucide-svelte/icons/file-plus-2';
	import AudioFileIcon from 'lucide-svelte/icons/file-volume';


	// This is sample data
	const data = {
		user: {
			name: 'Daniel Jyllikoski',
			email: 'daniel@jyllikoski.fi',
			avatar: '/useravatars/dj.png'
		},
		navMain: [
			{
				title: 'Haastattelut',
				url: '#',
				icon: AudioFileIcon,
				isActive: true
			},
			{
				title: 'Uusi',
				url: '#',
				icon: AddFile,
				isActive: false
			},
			{
				title: 'Roskakori',
				url: '#',
				icon: Trash2,
				isActive: false
			}
		],
		podcasts: [
			{
				podid: '1000694721078',
				name: 'HS Visio -podcast',
				date: '21.2.2025',
				subject: 'Eurooppa voi ratkaista sodan rahalla, vieraana Valtteri Ahti',
				teaser: ''
			},
			{
				podid: '1000694507711',
				name: 'Suomen nostatus',
				date: '20.2.2025',
				subject: 'Nyt Yhdysvallat tekee juuri sen, mitä toivomme',
				teaser: ''
			},
			{
				podid: '1000694237224',
				name: 'Futucast',
				date: '20.2.2025',
				subject: 'Tony Rehn | Muovia hiilidioksidista - miten päästöistä tehdään raaka-ainetta',
				teaser: ''
			},
			{
				podid: '1000690745960',
				name: 'Futucast',
				date: '10.2.2025',
				subject:
					'Ossi Kettunen | Arktisen alueen geopolitiikka: Trump, Grönlanti, Kiina, Venäjä ja Suomi',
				teaser: ''
			},
			{
				podid: '1000690742506',
				name: 'Startup-ministeriö',
				date: '10.2.2025',
				subject: 'Näin Supercell, Wolt ja Slush tekevät PR-työtä feat Heini Vesander',
				teaser: ''
			},
			{
				podid: '1000689947691',
				name: 'HS Visio -podcast',
				date: '7.2.2025',
				subject: 'Nvidia on suomalaisten kansanosake, vieraana Jukka Lepikkö',
				teaser: ''
			},
			{podid:"1000694985285", name: "Lauantaikerho", date: "22.2.2025", subject: "Vaalikevät sarastaa jo: Vaihtuuko valta Helsingissä? Lauantaikerho",teaser: "",},
			{podid:"1000695190411", name: "Ysärin lapset", date: "23.2.2025", subject: "Uusi minisarja kertoo 90-luvun kännäävistä nuorista",teaser: "",},
			{podid:"1000695009482", name: "inderesPodi", date: "22.2.2024", subject: "Tulosviikkosummaus (21.2.2025) | inderesPodi 222",teaser: "",},
			{podid:"1000695442653", name: "#neuvottelija Sami Miettinen", date: "24.2.2025", subject: "Trumpin ajan vientipolitiikka | Rydman",teaser: "",},			{podid:"1000694751482", name: "inderesPodi", date: "21.2.2025", subject: "Näkökulmia vastuulliseen sijoittamiseen osa 1, vieraana Vesa Puttonen ",teaser: "",},
			{podid:"1000695702568", name: "Väkevä elämä - Viisaampi mieli, vahvempi keho", date: "25.2.2025", subject: "Mikael Paajanen - Miten teet itsestäsi hybridiliikkujan, jolla on sekä voimaa että kestävyyttä?",teaser: "",},
			{podid:"1000695422901", name: "Mimmit sijoittaa", date: "24.2.2025", subject: "K3 J2: Kannattaako NYT ostaa (sijoitus)asunto? Ekonomisti vastaa",teaser: "",},
			{podid:"1000695440009", name: "Futucast", date: "24.2.2025", subject: "Jyri Kosola | Tulevaisuuden sotateknologia #517",teaser: "",},
			{podid:"1000694633694", name: "Politiikan viikko", date: "21.2.2025", subject: "Jakso 17: Ukrainasta ilman Ukrainaa",teaser: "",},
			{podid:"1000694811790", name: "Mikä meitä vaivaa?", date: "21.2.2025", subject: "Jakso 121: Latistuksen mankeli",teaser: "",},
			{podid:"1000695645737", name: "Seinä kolmannelle", date: "24.2.2025", subject: "Brittifutispodcast: Mestaruustaisto on päättynyt",teaser: "",},
			{podid:"1000695364559", name: "Puurojengi", date: "23.2.2025", subject: "86. Etikettikoulu",teaser: "",},
			{podid:"1000694151332", name: "Puurojengi", date: "19.2.2025", subject: "85. Vältyin täpärästi kiroukselta",teaser: "",},
			{podid:"1000695641515", name: "Bella Table", date: "24.2.2025", subject: "218. Ihaninta just nyt",teaser: "",},
			{podid:"1000695413973", name: "Psykopodiaa", date: "24.2.2025", subject: "174. Tyhmä työelämä. Vieraana Mona Moisala.",teaser: "",},
			{podid:"1000695735266", name: "Sijoituskästi", date: "25.2.2025", subject: "#207 Onko Trump seonnut? ft. Tero Kuittinen",teaser: "",},
			// {podid:"1000694012385", name: "Amerikkapodi", date: "19.2.2025", subject: "MAGA-aalto löi Eurooppaan, J. D. Vance etsii aate­veljiä",teaser: "",},
			// {podid:"1000693832063", name: "Elä viitti!", date: "19.2.2025", subject: "J65: Itse itsensä Islannin johtajaksi nimittänyt seikkailija",teaser: "",},
			// {podid:"1000689442113", name: "Politbyroo", date: "5.2.2025", subject: "Halliksen puhemiesvaali; metsät, päästöt ja Multala; Trumpin kauppasota ja muut hommelit - 5.2.2025", teaser: "",}
		]
	};
</script>

<script lang="ts">
	import NavUser from '$lib/components/nav-user.svelte';
	import { Label } from '$lib/components/ui/label/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { useSidebar } from '$lib/components/ui/sidebar/index.js';
	import { Switch } from '$lib/components/ui/switch/index.js';
	import Command from 'lucide-svelte/icons/command';
	import type { ComponentProps } from 'svelte';
	import { goto } from '$app/navigation'; // Import SvelteKit's goto function

	let { ref = $bindable(null), ...restProps }: ComponentProps<typeof Sidebar.Root> = $props();

	let activeItem = $state(data.navMain[0]);
	let podcasts = $state(data.podcasts);
	const sidebar = useSidebar();

	function navigateTo(path: string) {
		goto(path);
	}
</script>

<Sidebar.Root
	bind:ref
	collapsible="icon"
	class="overflow-hidden [&>[data-sidebar=sidebar]]:flex-row"
	{...restProps}
>
	<!-- This is the first sidebar -->
	<!-- We disable collapsible and adjust width to icon. -->
	<!-- This will make the sidebar appear as icons. -->
	<Sidebar.Root collapsible="none" class="!w-[calc(var(--sidebar-width-icon)_+_1px)] border-r">
		<Sidebar.Header>
			<Sidebar.Menu>
				<Sidebar.MenuItem>
					<Sidebar.MenuButton size="lg" class="md:h-8 md:p-0">
						{#snippet child({ props })}
							<a href="##" {...props}>
								<div
									class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground"
								>
									<Command class="size-4" />
								</div>
								<div class="grid flex-1 text-left text-sm leading-tight">
									<span class="truncate font-semibold">Kohtain</span>
									<span class="truncate text-xs"></span>
								</div>
							</a>
						{/snippet}
					</Sidebar.MenuButton>
				</Sidebar.MenuItem>
			</Sidebar.Menu>
		</Sidebar.Header>
		<Sidebar.Content>
			<Sidebar.Group>
				<Sidebar.GroupContent class="px-1.5 md:px-0">
					<Sidebar.Menu>
						{#each data.navMain as item (item.title)}
							<Sidebar.MenuItem>
								<Sidebar.MenuButton
									tooltipContentProps={{
										hidden: false
									}}
									onclick={() => {
										activeItem = item;
										sidebar.setOpen(true);
									}}
									isActive={activeItem.title === item.title}
									class="px-2.5 md:px-2"
								>
									{#snippet tooltipContent()}
										{item.title}
									{/snippet}
									<item.icon />
									<span>{item.title}</span>
								</Sidebar.MenuButton>
							</Sidebar.MenuItem>
						{/each}
					</Sidebar.Menu>
				</Sidebar.GroupContent>
			</Sidebar.Group>
		</Sidebar.Content>
		<Sidebar.Footer>
			<NavUser user={data.user} />
		</Sidebar.Footer>
	</Sidebar.Root>

	<!-- This is the second sidebar -->
	<!-- We disable collapsible and let it fill remaining space -->
	<Sidebar.Root collapsible="none" class="hidden flex-1 md:flex">
		<Sidebar.Header class="w-max-[40ch] gap-3.5 border-b p-4">
			<div class="flex w-full items-center justify-between">
				<div class="text-base font-medium text-foreground">
					{activeItem.title}
				</div>
			</div>
			<Sidebar.Input placeholder="Haku teksteistä (olisi varmaan hyvä)" />
		</Sidebar.Header>
		<Sidebar.Content class="overflow-y-auto overflow-x-clip">
			<Sidebar.Group class="px-0">
				<Sidebar.GroupContent>
					{#each podcasts as podcast (podcast.podid)}
						<a
							href="/transcript/{podcast.podid}"
							data-sveltekit-preload-data="hover"
							data-sveltekit-reload
							class="flex flex-col items-start gap-2 whitespace-nowrap border-b p-4 text-sm leading-tight last:border-b-0 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
						>
							<div class="flex w-[260px] items-center gap-2">
								<span>{podcast.name}</span>{' '}
								<span class="ml-auto text-xs">{podcast.date}</span>
							</div>
							<span class="w-[260px] whitespace-break-spaces text-xs">{podcast.subject}</span>
							<!-- <span class="line-clamp-2 w-[260px] whitespace-break-spaces text-xs">
								{mail.teaser}
							</span> -->
						</a>
					{/each}
				</Sidebar.GroupContent>
			</Sidebar.Group>
		</Sidebar.Content>
	</Sidebar.Root>
</Sidebar.Root>
