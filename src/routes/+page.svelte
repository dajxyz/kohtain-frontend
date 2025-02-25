<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<div class="emoji-cycle"></div>



<style>
    .emoji-cycle::after {
        content: "🌍";
        animation: cycleEmojis 60s infinite steps(1);
        animation-timing-function: ease-in;
    }

    @keyframes cycleEmojis {
        0% { content: "🌍"; opacity: 1 }
        8% { content: "🌍"; opacity: 1 }
        /* 8.2% { content: "🌍"; opacity: 0 } */

        /* 8.3% { content: "🌎"; opacity: 0 }
        10% { content: "🌎"; opacity: 1 }
        19% { content: "🌎"; opacity: 1 }
        19.2% { content: "🌎"; opacity: 0 }

        19.3% { content: "🌏"; opacity: 0  }
        22% { content: "🌏"; opacity: 1  }
        30% { content: "🌏"; opacity: 1  }
        30.2% { content: "🌏"; opacity: 0  } */

        20% { content: "🌍"; opacity: 1 }
        20.2% { content: "🌍"; opacity: 0 }

        20.4% { content: "🇫🇮"; opacity: 0 }
        23% { content: "🇫🇮"; opacity: 1  }
        /* 41% { content: "🇫🇮"; opacity: 1  } */
        /* 41.2% { content: "🇫🇮"; opacity: 0 } */

        /* 41.3% { content:  "🇸🇪"; opacity: 0 } */
        33% { content: "🇸🇪"; opacity: 1  }
        /* 42% { content: "🇸🇪"; opacity: 1  }
        43% { content:  "🇸🇪"; opacity: 0 }  */


        /* 52.3% { content:  "🇦🇽"; opacity: 0 } */
        43% { content: "🇦🇽"; opacity: 1  }
        53% { content: "🇦🇽"; opacity: 1  }
        53.2% { content:  "🇦🇽"; opacity: 0 }

        53.3% { content: "🌍"; opacity: 0 }
        54% { content: "🌍"; opacity: 1 }
        64% { content: "🌍"; opacity: 1 }
        64.3% { content: "🌍"; opacity: 0 }


        64.5% { content: "🇬🇧"; opacity: 0 }
        66% { content: "🇬🇧"; opacity: 1 }
        /* 74% { content: "🇬🇧"; opacity: 1 }
        74.2% { content: "🇬🇧"; opacity: 0 } */

        /* 74.3% { content: "🇮🇪"; opacity: 0 } */
        77% { content: "🇮🇪"; opacity: 1 }
        /* 89% { content: "🇮🇪"; opacity: 1 } */
        /* 89.2% { content: "🇮🇪"; opacity: 0 } */

        /* 89.3% { content: "🇲🇹"; opacity: 0 }  */
        88% { content: "🇲🇹"; opacity: 1 }
        /* 98% { content: "🇲🇹"; opacity: 1 } */
        94% { content: "🇲🇹"; opacity: 0 } 

        95% { content: "🌍"; opacity: 0 } 
        96% { content: "🌍"; opacity: 1 }

    }

    .emoji-cycle {
        font-size: 3rem;
        font-family: sans-serif;
    }
</style>