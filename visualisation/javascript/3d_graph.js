const load = function(graph, fname) {
	graph
		// .resetProps() // Wipe current state
		.cooldownTicks(200) // How long before positions freeze
		// .onEngineStop(() => graph.zoomToFit(400))
		.nodeLabel("id")
		.linkLabel("value")
		.nodeAutoColorBy("group")
		.nodeThreeObject(node => {
			const sprite = new SpriteText(node.id);
			sprite.color = node.color;
			sprite.textHeight = 12;
			return sprite;
		  })
		// .forceEngine("d3-force-3d") // Either d3-force-3d or ngraph
		.nodeOpacity(1)
		.linkOpacity(1)
		.linkWidth("1px")
		// .linkDirectionalArrowLength(5)
		// .linkDirectionalArrowRelPos(1)
		.linkDirectionalParticles(2)
		.linkCurvature(0.25)
		.jsonUrl(fname);
};

// From https://github.com/vasturiano/3d-force-graph
const graph = ForceGraph3D()(document.getElementById("graph_canvas"))
graph
	.backgroundColor("#000")
	.showNavInfo(false)

load(graph, "data/test_graph.json");