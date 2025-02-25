let position = $state(0);

export function getPositioner(to) {
	
	function set(to) {
		position = to;
	}

	return {
		get position() {
			return position;
		},
		set
	};
}