export default defineAppConfig({
  ui: {
    // The PandaDev palette (Radix) is applied in assets/css/main.css, which overrides the
    // Nuxt UI design tokens (--ui-primary, --ui-bg, --ui-text…). These Tailwind scales are only
    // a fallback for the few classes that use a numbered shade: closest ones to the palette.
    colors: {
      primary: 'red',
      neutral: 'slate'
    },

    // Primary color rendered like the Radix components: Nuxt UI derives everything from one
    // color with opacities, Radix uses a dedicated step per role (accent-* classes, main.css):
    // solid 9 / hover 10, soft a3 / hover a4 / pressed a5, borders a7-a8, text 11.
    button: {
      compoundVariants: [
        { color: 'primary', variant: 'solid', class: 'hover:bg-accent-10 active:bg-accent-10 outline-accent-8' },
        { color: 'primary', variant: 'outline', class: 'ring-accent-a8 text-accent-11 hover:bg-accent-a2 active:bg-accent-a3 outline-accent-8 focus-visible:ring-accent-8' },
        { color: 'primary', variant: 'soft', class: 'text-accent-11 bg-accent-a3 hover:bg-accent-a4 active:bg-accent-a5 disabled:bg-accent-a3 aria-disabled:bg-accent-a3 outline-accent-8' },
        { color: 'primary', variant: 'subtle', class: 'text-accent-11 ring-accent-a7 bg-accent-a3 hover:bg-accent-a4 active:bg-accent-a5 disabled:bg-accent-a3 aria-disabled:bg-accent-a3 outline-accent-8 focus-visible:ring-accent-8' },
        { color: 'primary', variant: 'ghost', class: 'text-accent-11 hover:bg-accent-a3 active:bg-accent-a4 outline-accent-8' },
        { color: 'primary', variant: 'link', class: 'text-accent-11 hover:text-accent-12 active:text-accent-12 disabled:text-accent-11 aria-disabled:text-accent-11 outline-accent-8' }
      ]
    },
    badge: {
      compoundVariants: [
        { color: 'primary', variant: 'outline', class: 'text-accent-11 ring-accent-a8' },
        { color: 'primary', variant: 'soft', class: 'bg-accent-a3 text-accent-11' },
        { color: 'primary', variant: 'subtle', class: 'bg-accent-a3 text-accent-11 ring-accent-a7' }
      ]
    },
    link: {
      variants: {
        active: {
          true: 'text-accent-11'
        }
      }
    },
    navigationMenu: {
      compoundVariants: [
        { color: 'primary', active: true, class: { link: 'text-accent-11', linkLeadingIcon: 'text-accent-11 group-data-[state=open]:text-accent-11' } }
      ]
    }
  }
})
