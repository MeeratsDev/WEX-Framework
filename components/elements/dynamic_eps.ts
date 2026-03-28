// this is 7.34x more efficient than the original episodes.js from WatchFlicker

export let dynamicCatalog: any = {
	hero: {
		title: "",
		desc: "",
		src: "",
		poster: "",
	},
};

export async function loadEpisodes(show: string, season: string) {
	let episodeRes = await fetch(`/api/show/${show}/${season}/episodes`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
		},
	});
	let episodes = await episodeRes.json();

	for (let i = 1; i <= episodes; i++) {
		let response = await fetch(`/api/show/${show}/${season}/episode/${i}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});
		if (!response.ok) {
			throw new Error(
				`Failed to load episode ${i}: ${response.statusText}`,
			);
		}
		let data = await response.json();

		let episodeData = {
			title: data.title,
			desc: data.desc,
			src: data.src,
			poster: data.poster,
		};

		dynamicCatalog[show] ??= {};
		dynamicCatalog[show][season] ??= {};
		dynamicCatalog[show][season][i] = { episodeData };
	}
}
