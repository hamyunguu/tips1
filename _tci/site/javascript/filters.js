const container = document.querySelector("#explore-filters")
const filters = document.querySelectorAll('#explore-filters__filters button');
const label = document.querySelector('#explore-filters__label');
const blocks = document.querySelectorAll(".box")

function handleClick(event) {
  if (event.target.classList.contains("active")) {
    event.target.classList.remove("active")
    reset()
  } else {
    filters.forEach(filter => filter.classList.remove("active"))
    event.target.classList.add("active")

    const type = event.target.dataset.type
    const term = event.target.dataset.filter
    const label = event.target.innerHTML

    filterBlocks(type + "s", term)
    setLabel(label)
    insertUrlParam(type, term);
  }

  container.open = false;
}

function filterBlocks(type, term) {
  blocks.forEach(block => {
    const blockType = block.dataset[type]

    if (blockType === undefined || !blockType.includes(term)) {
      block.classList.add("hidden")
    } else {
      block.classList.remove("hidden")
    }
  })
}

function reset() {
  // Remove 'hidden' from all blocks except those with data-languages,
  // which are translations and hidden by default
  blocks.forEach(block => {
    if (block.dataset.languages) { 
      block.classList.add("hidden")
    } else {
      block.classList.remove("hidden")
    }
  })

  setLabel("")

  const url = new URL(location);
  url.search = null;
  history.replaceState(null, "", window.location.pathname)
}

function setLabel(string) {
  label.innerHTML = string
}

function insertUrlParam(key, value) {
  const url = new URL(location)

  url.searchParams.set("type", key)
  url.searchParams.set("filter", value)
  history.replaceState(null, "", url)
}

function load() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  if (urlParams.has('type') && urlParams.has('filter')) {
    const filter_param = urlParams.get('filter');
    const target = Array.from(filters).find(filter => filter.dataset.filter === filter_param)

    if (target) { 
      target.click()
    }
  }
}

filters.forEach(filter => filter.addEventListener("click", handleClick))
load()