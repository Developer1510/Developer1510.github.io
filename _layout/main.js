var isSearchDisplayed = false;

function toggleSearch() {
	isSearchDisplayed = !isSearchDisplayed;
	document.getElementById("sidebar-search").className = isSearchDisplayed ? 'visible' : 'hidden';
	if (!isSearchDisplayed) {
		document.getElementById("search-box").value = '';
	}
	performSearch('');
}

function searchKeyDown(searchElement) {
	if (event.key === 'Enter') {
		performSearch(searchElement.value);        
    }
}

function performSearch(searchValue) {
	for (var groupId in groups) {
		var group = groups[groupId];
		var pins = group['pins'];
		var currIndex = group['index'];
		if (currIndex == undefined) {
			currIndex = 0;
		}
		
		for (var pinIndex in pins) {
			var pin = pins[pinIndex];
			pin['visible'] = (stringMatch(pin['title'], searchValue) || stringMatch(pin['description'], searchValue)) ? 'true' : 'false';
		}
		
		if (pins[currIndex]['visible'] != 'true') {
			currIndex = getNextVisiblePin(groupId, currIndex);
		}
		updatePin(groupId, group, currIndex);
	}
}

function stringMatch(haystack, needle) {
	if (!needle) {
		return true;
	}
	if (!haystack) {
		return false;
	}
	
	haystack = haystack.toLowerCase();
	var tokens = needle.toLowerCase().split(' ');
	for (var i in tokens) {
		var token = tokens[i];
		if ((token.length > 0) && !haystack.includes(token)) {
			return false;
		}
	}
	return true;
}

function pinLeft(groupId) {
	var group = groups[groupId];
	var currIndex = group['index']
	if (currIndex == undefined) {
		currIndex = 0;
	}
	currIndex = getPrevVisiblePin(groupId, currIndex)
	updatePin(groupId, group, currIndex);
}

function pinRight(groupId) {
	var group = groups[groupId];
	var currIndex = group['index']
	if (currIndex == undefined) {
		currIndex = 0;
	}
	currIndex = getNextVisiblePin(groupId, currIndex)
	updatePin(groupId, group, currIndex);
}

function getGroupPinsCount(groupId) {
	var count = 0;
	var pins = groups[groupId]['pins'];
	for (var pinIndex in pins) {
		var pin = pins[pinIndex];
		if (pin['visible'] == 'true') {
			count++;
		}
	}
	return count;
}

function getPrevVisiblePin(groupId, currIndex) {
	var pins = groups[groupId]['pins'];
	while (currIndex > 0) {
		currIndex--;
		if (pins[currIndex]['visible'] == 'true') {
			return currIndex;
		}
	}
	return 0;
}

function getNextVisiblePin(groupId, currIndex) {
	var pins = groups[groupId]['pins'];
	while (currIndex < pins.length - 1) {
		currIndex++;
		if (pins[currIndex]['visible'] == 'true') {
			return currIndex;
		}
	}
	return getPrevVisiblePin(groupId, currIndex);
}

function updatePin(groupId, group, currIndex) {
	group['index'] = currIndex;
	var pinCount = getGroupPinsCount(groupId);
	document.getElementById(groupId + '-left').style.display = (currIndex > 0) ? 'block' : 'none';
	document.getElementById(groupId + '-right').style.display = (currIndex < pinCount - 1) ? 'block' : 'none';
	
	var pins = group['pins'];
	var pin = pins[currIndex];
	
	document.getElementById(groupId + '-container').style.display = (pinCount > 0) ? 'block' : 'none';
	document.getElementById(groupId + '-title').innerHTML = pin['title'];
	document.getElementById(groupId + '-image-path').src = pin['thumbnail_path'];
	document.getElementById(groupId + '-date').innerHTML = pin['date'];
	document.getElementById(groupId + '-type').innerHTML = pin['type'];
	document.getElementById(groupId + '-eob').href = pin['eob_url'];
	document.getElementById(groupId + '-eob').style.display = pin['eob_url'] ? 'block' : 'none';
	document.getElementById(groupId + '-download').href = pin['download_url'];
	document.getElementById(groupId + '-download').style.display = pin['download_url'] ? 'block' : 'none';
	document.getElementById(groupId + '-description').innerHTML = pin['description'];
			
	var worldMarker = document.getElementById(groupId + '-world-marker');
	worldMarker.style.left = pin['world_pos_x'] + 'px'; 
	worldMarker.style.top = pin['world_pos_y'] + 'px';
	
	if (pins.length > 1) {
		for (var i = 0; i < pins.length; i++) {
			document.getElementById(groupId + '_pin' + i).src = layoutDir + 'pager_' + ((i == currIndex) ? 'current' : 'other') + '.png'; 
		}
	}
}
