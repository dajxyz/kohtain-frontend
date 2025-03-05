let position = $state(0);

export function getPositioner() {
	
	function set(to: number) {
		position = to;
	}

	return {
		get position() {
			return position;
		},
		set
	};
}
