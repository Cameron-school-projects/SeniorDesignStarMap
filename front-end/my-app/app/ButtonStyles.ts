
import { tv } from 'tailwind-variants';

//button display config stuff
export const baseButton = tv({
  base: 'text-center relative font-semibold whitespace-nowrap align-middle outline-none inline-flex items-center justify-center select-none',
  variants: {
    size: {
      xs: 'text-xs py-1 px-2',
      md: 'text-sm py-2 px-4',
      lg: 'text-base py-3 px-6',
      xl: 'text-lg py-4 px-8',
      xxl: 'text-xl py-5 px-10',
      square_xs: 'text-xs h-4 w-4 p-1',
      square_sm: 'text-sm h-6 w-6 p-1',
      square_md: 'text-base h-8 w-8 p-1',
      square_lg: 'text-lg h-10 w-10 p-1',
      square_xl: 'text-xl h-12 w-12 p-1',
    },
    vPadding: {
      xs: 'py-[4px]',
      sm: 'py-[8px]',
      md: 'py-[12px]',
      lg: 'py-[16px]',
    },
    vSpace: {
      xs: 'my-1',
      sm: 'my-2',
      md: 'my-4',
      lg: 'my-6',
    },
    HSpace: {
      xs: 'mx-1',
      sm: 'mx-2',
      md: 'mx-4',
      lg: 'mx-6',
    },
    align: {
      center: 'mx-auto',
      right: 'ml-auto',
      left: 'mr-auto',
      top: 'mb-auto',
      bottom: 'mt-auto',
    },
    rounded: {
      none: 'rounded-none',
      xs: 'rounded-[2px]',
      sm: 'rounded-[4px]',
      normal: 'rounded-[8px]',
      lg: 'rounded-[12px]',
      full: 'rounded-full',
    },
    behavior: {
      block: 'w-full',
    },
  },
});

// create solid button styles
export const solidButton = tv({
  extend: baseButton,
  variants: {
    color: {
      green:
        'bg-[#58cc02] text-gray-100 shadow active:shadow-none active:translate-y-[5px]',
      teal: 'bg-[#0D9488] text-gray-100 shadow-teal active:shadow-none active:translate-y-[5px]',
      yellow:
        'bg-[#FFC700] text-gray-100 shadow-yellow active:shadow-none active:translate-y-[5px]',
      gray: 'bg-[#64748B] text-gray-100 shadow-blueGray active:shadow-none active:translate-y-[5px]',
    },
  },
});