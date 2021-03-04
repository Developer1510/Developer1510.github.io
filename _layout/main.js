var isSearchDisplayed = false;

function toggleSearch() {
	isSearchDisplayed = !isSearchDisplayed;
	document.getElementById("sidebar-search").className = isSearchDisplayed ? 'visible' : 'hidden';
	if (!isSearchDisplayed) {
		document.getElementById("sidebar-search").value = '';
	}
	performSearch('');
}

function searchKeyDown(searchElement) {
	if (event.key === 'Enter') {
		performSearch(searchElement.value);        
    }
}

function performSearch(searchValue) {
	
}

function pinLeft(groupId) {
	var group = groups[groupId];
	var currIndex = group['index']
	if (currIndex == undefined) {
		currIndex = 0;
	}
	if (currIndex > 0) {
		currIndex--;
	}
	updatePin(groupId, group, currIndex);
}

function pinRight(groupId) {
	var group = groups[groupId];
	var currIndex = group['index']
	if (currIndex == undefined) {
		currIndex = 0;
	}
	if (currIndex < group['pins'].length - 1) {
		currIndex++;
	}
	updatePin(groupId, group, currIndex);
}

function updatePin(groupId, group, currIndex) {
	group['index'] = currIndex;
	var pinCount = group['pins'].length;
	document.getElementById(groupId + '-left').style.display = (currIndex > 0) ? 'block' : 'none';
	document.getElementById(groupId + '-right').style.display = (currIndex < pinCount - 1) ? 'block' : 'none';
	
	var pin = group['pins'][currIndex];
	
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
	
	for (var i = 0; i < pinCount; i++) {
		document.getElementById(groupId + '_pin' + i).src = layoutDir + 'pager_' + ((i == currIndex) ? 'current' : 'other') + '.png'; 
	}
}
