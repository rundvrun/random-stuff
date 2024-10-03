const db = new Dexie('ImageCache');
db.version(1).stores({
	images: 'url, blob'
});
var hostImg = ""; // use cookie instead

async function saveImageIndexedDB(src) {
	const key = { url: src };
	let data = await db.images.get(key);
	if (!data) {
		data = await fetchImageToBlob(src);
		db.images.add(data);  // dont need await save, just render immediately
	}
	return data;
}

async function applyXSrcIndexedDB(sender, ignoreFetched=false) {
	try {
		if (sender.src && ignoreFetched) return;
		const imgs = [...document.querySelectorAll("img[data-x-src]")].filter(t => t.dataset.xSrc == sender.dataset.xSrc);
		let data = await saveImageIndexedDB(sender.dataset.xSrc);
		await renderBlob(imgs, data.blob);
	}
	catch (e) {
		console.log(e)
	}
}

async function applyXSrcIndexedDBCanvas(sender, ignoreFetched=false) {
	try {
		if (sender.src && ignoreFetched) return;
		const key = { url: sender.dataset.xSrc };
		const imgs = [...document.querySelectorAll("img[data-x-src]")].filter(t => t.dataset.xSrc == key.url);
		let data = await db.images.get(key);
		if (!data) {
			return fakeImg(sender).onload = (e) => getCanvas(e.target).toBlob(async (b) => {
				db.images.add({ url: key.url, blob: b });
				await renderBlob(imgs, b);
			});
		}
		await renderBlob(imgs, data.blob);
	}
	catch (e) {
		console.log(e)
	}
}

async function renderBlob(imgs, b) {
	const u = URL.createObjectURL(b);
	try {
		await Promise.allSettled([...imgs].map(img => {
			return new Promise((res, rej) => {
				function er() {
					img.removeEventListener("error", er);
					rej();
				}
				img.src = u;
				img.addEventListener("load", function l() {
					img.removeEventListener("load", l);
					img.removeEventListener("error", er);
					img.removeAttribute("data-x-src"); // hide it :))
					res();
				});
				img.addEventListener("error", er);
			});
		}));
	}
	catch (e) {
		console.log(e);
	}
	finally {
		URL.revokeObjectURL(u);
	}
}

function applyXSrcLocalStorage(target) {
	let imgSrc = target.dataset.xSrc;
	let data = localStorage.getItem(imgSrc);
	if (data) {
		setNewSrc(imgSrc, data);
	}
	else {
		fakeImg(target).addEventListener("load", imageReceivedLocalStorage, false);
	}
}

function imageReceivedLocalStorage(e) {
	let sender = e.target;
	const canvas = getCanvas(sender);
	try {
		sender.removeEventListener("load", imageReceivedLocalStorage);
		let data = canvas.toDataURL("image/png");
		localStorage.setItem(sender.origin.dataset.xSrc, data);
		setNewSrc(sender.origin.dataset.xSrc, data);
  	} catch (err) {
		console.error(`Error: ${err}`);
	}
}

function setNewSrc(xSrc, src) {
	[...document.querySelectorAll("img[data-x-src]")].filter(t => t.dataset.xSrc == xSrc).forEach(img => {
		img.src = src;
		img.removeAttribute("data-x-src");
	});
}

function fakeImg(target) {
	let imgSrc = target.dataset.xSrc;
	let img = new Image();
	img.origin = target;
	img.crossOrigin = "anonymous"; // canvas need it
	img.src = hostImg + imgSrc;
	return img;
}

function fetchImageToBlob(src) {
	return fetch(hostImg + src)
	.then(response => response.blob())
	.then(b => Object({ url: src, blob: b }));
}

function getCanvas(sender) {
	const canvas = document.createElement("canvas");
	const context = canvas.getContext("2d");
	canvas.width = sender.width;
	canvas.height = sender.height;
	context.drawImage(sender, 0, 0);
	return canvas;
}

function fetchImgOnLoad(ignoreFetched=true) {
	const imgGroup = Object.groupBy(document.querySelectorAll("img[data-x-src]"), i => i.dataset.xSrc);
	//Object.keys(imgGroup).map(src => imgGroup[src][0]).forEach(applyXSrcLocalStorage);
	Object.keys(imgGroup).map(src => imgGroup[src][0]).forEach(i => applyXSrcIndexedDB(i, ignoreFetched));
}
fetchImgOnLoad();

let lsSize = new Blob(Object.values(localStorage)).size;
