'use strict'

$('.ui.dropdown').dropdown();
$('.ui.search').search({
	type: 'category',
	apiSettings: {
		url: '/search?query={query}&format=sui'
	},
});

console.log('end liftree layout');