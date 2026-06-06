const searchResultsContainer = document.querySelector('#search-results')
const noResultsContainer = document.querySelector('.no-results')

const search = instantsearch({
  indexName: 'tci_v2',
  searchClient: algoliasearch('BR7W05XB5G', 'e53a8465ffdeeb730fbc45160e984f65'),
  routing: true,
  searchParameters: {
    restrictSearchableAttributes: [
      'title',
      'content',
      'author',
      'first_name',
      'last_name'
    ]
  },

  searchFunction: function (helper) {
    if (helper.state.query === '') {
      searchResultsContainer.style.display = 'none'
      noResultsContainer.style.display = 'block'
    } else {
      helper.search()
      searchResultsContainer.style.display = 'block'
      noResultsContainer.style.display = 'none'
    }
  }
})

const hitTemplate = function (hit) {
  const url = hit.url
  const title = hit._highlightResult.title.value
  const content =
    typeof hit._highlightResult.content === 'undefined'
      ? ''
      : hit._highlightResult.content.value
  const date =
    typeof hit.date === 'undefined'
      ? ''
      : dayjs.unix(hit.date).format('MMM D, YYYY')
  const image =
    typeof hit.crop_image === 'undefined'
      ? ''
      : `<img class="search-crop-image" style="max-width:20px;" src="${hit.crop_image.includes('https')
        ? hit.crop_image
        : 'https://cdn.filestackcontent.com/resize=width:80/' +
        hit.crop_image
      }" />`

  return `
    <div class="result-item">
      <h2><a class="post-link" href="${url}">${title} ${image}</h2>
      <div class="search-date">${date}</div>
      <div class="search-post-snippet">
        <p>${content}</p>
      </div>
      <div class="clearer"></div>
    </div>
  `
}

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#search-searchbar',
    placeholder: '...'
  }),

  instantsearch.widgets.infiniteHits({
    container: '#search-results',
    templates: {
      empty:
        'Sorry, we couldn\'t anything matching your search. You can always view everything on TCI in the <a href="/archive">archive</a>. <div class="search-snail"></div>',
      showMoreLabel: 'More results',
      item: hitTemplate
    }
  })
])

search.start()

const searchDialog = document.getElementById('search')
const searchButton = document.getElementById('search-button')
const closeSearchButton = document.getElementById('close-search')
const searchInput = document.querySelector('.ais-SearchBox-input')

function openSearch() {
  searchDialog.classList.add('open')
  document.body.style.position = "fixed"
  window.addEventListener("keydown", handleEscPress)
}

function handleEscPress(event) {
  if (event.key === "Escape") {
    closeSearch()
  }
}

function closeSearch() {
  searchDialog.classList.remove('open')
  document.body.style.position = null
  searchInput.focus()
  window.scrollTo(0, 0)

  const clean_uri = location.protocol + '//' + location.host + location.pathname
  window.history.replaceState({}, document.title, clean_uri)

  window.removeEventListener("keydown", handleEscPress)
}

if (searchButton) {
  searchButton.addEventListener('click', openSearch)
}

if (closeSearchButton) {
  closeSearchButton.addEventListener('click', closeSearch)
}

if (window.location.href.indexOf('?tci_v2%5Bquery%5D=') > -1) {
  openSearch()
}
