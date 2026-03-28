export function changeTheme(themeName: string) {
    document.documentElement.style.setProperty(`--backgroundColour`, `var(--backgroundColour${themeName})`);
    document.documentElement.style.setProperty(`--borderColour`, `var(--borderColour${themeName})`);
    document.documentElement.style.setProperty(`--textColour`, `var(--textColour${themeName})`);
    document.documentElement.style.setProperty(`--heroGradient`, `var(--heroGradient${themeName})`);
    document.documentElement.style.setProperty(`--longGradient`, `var(--longGradient${themeName})`);
    document.documentElement.style.setProperty(`--navGradient`, `var(--navGradient${themeName})`);
    document.documentElement.style.setProperty(`--panel`, `var(--panel${themeName})`);
    document.documentElement.style.setProperty(`--episodeHover`, `var(--episodeHover${themeName})`);
}
