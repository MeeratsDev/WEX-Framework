// taken straight from the WatchFlicker codebase

export function darkMode() {
    document.documentElement.style.setProperty('--backgroundColour', 'var(--backgroundColourDark)');
    document.documentElement.style.setProperty('--borderColour', 'var(--borderColourDark)');
    document.documentElement.style.setProperty('--textColour', 'var(--textColourDark)');
    document.documentElement.style.setProperty('--heroGradient', 'var(--heroGradientDark)');
    document.documentElement.style.setProperty('--longGradient', 'var(--longGradientDark)');
    document.documentElement.style.setProperty('--navGradient', 'var(--navGradientDark)');
    document.documentElement.style.setProperty('--panel', 'var(--panelDark)');
    document.documentElement.style.setProperty('--episodeHover', 'var(--episodeHoverDark)');
}

export function lightMode() {
    document.documentElement.style.setProperty('--backgroundColour', 'var(--backgroundColourLight)');
    document.documentElement.style.setProperty('--borderColour', 'var(--borderColourLight)');
    document.documentElement.style.setProperty('--textColour', 'var(--textColourLight)');
    document.documentElement.style.setProperty('--heroGradient', 'var(--heroGradientLight)');
    document.documentElement.style.setProperty('--longGradient', 'var(--longGradientLight)');
    document.documentElement.style.setProperty('--navGradient', 'var(--navGradientLight)');
    document.documentElement.style.setProperty('--panel', 'var(--panelLight)');
    document.documentElement.style.setProperty('--episodeHover', 'var(--episodeHoverLight)');
}
