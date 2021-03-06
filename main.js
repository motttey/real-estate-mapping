function plotAllEstate(projection){

  for (let i = 0; i < city_length; i++) {
      let id = ('000' + i).slice(-3);
      // if (i!== 29 && visible_towns.indexOf(i) > 0) {
      if (i!== 29 && i!== 40 && i!== 42) {
        plotCoordinates(projection, "./json/output"+id+".json", i, red_gray_grad(i/city_length));
      }
  }

  // 下位をマッピング
  const min_index = city_length + 1;
  const lowest_num = city_max + 1;
  for (var i = min_index; i < lowest_num; i++) {
      let id = ('000' + i).slice(-3);
      if (i!== 117 && i!== 75) {
        plotCoordinates(projection, "./json/output"+id+".json", i, green_gray_grad( (lowest_num - i) / (lowest_num - min_index) ));
      }
  }
}

function plotPrefecture(id, projection, price_max){
  $.get("./JapanCityGeoJson/geojson/prefectures/"+('00' + id).slice(-2)+".json", function(data){
      let data_parsed = $.parseJSON(data);
      let geoPath = d3.geoPath().projection(projection);

      let prefecture_group =  d3.select("svg").append("g").attr("class", "prefecture_g")

      let price_data;

      // JSONにしてオブジェクト単位で取れるようにする
      d3.json("./json/price.json").then(function(p_data){
         price_data = p_data;

         let map = prefecture_group.selectAll("path")
           .data(data_parsed.features)
           .enter()
           .append("path")
             .attr("d", geoPath)
             .attr("id", function(d){ return d.id; })
             .style("stroke", "gray")
             .style("stroke-width", 1);

         prefecture_group.selectAll("path").each(function(d,i){
           d3.select(this).style("fill", function(){
             if (d.id.toString() in price_data) return while_blue_grad(parseInt(price_data[d.id].price)/price_max);
             else return "black";
           })
         });
      });

  });
}

function plotRailPath(projection, station_list, color) {
  let projected_coordinate = [];
  station_list.forEach(function(d){
    projected_coordinate.push(projection([d["lng"], d["lat"]]));
  });

  let line = d3.line()
      .x(function(d) {return d[0];})
      .y(function(d) {return d[1];});

  let line_g = d3.select("#anotation").append('g')
      .attr('class', 'rails_line');

  let path = line_g.append('path')
      .attr("d", line(projected_coordinate))
      .attr("stroke", color)
      .attr("fill", "none")
      .attr("opacity", 0.5)
      .attr("stroke-width", 5);
}

function plotStations(projection, stations) {
  let projected_coordinate = [];
  stations.forEach(function(d){
    projected_coordinate.push(projection([d["lng"], d["lat"]]));
  });

  let circles_g = d3.select("#anotation").append('g')
      .attr('id', 'stations_circle');

  let circles = circles_g.selectAll('.stations_circle')
      .data(projected_coordinate)
      .enter()
      .append('circle')
      .attr('class', 'stations_circle')
      .attr('cx', function(d){
        return d[0];
      })
      .attr('cy', function(d){
        return d[1];
      })
      .attr('r', kilometor)
      .attr('stroke', "gray")
      .attr('fill', "none")
      .style('opacity', '0.5');

  let text = circles_g.selectAll('.stations_text')
      .data(projected_coordinate)
      .enter()
      .append("text")
      .attr('class', 'stations_text')
      .attr('x', function(d){
        return d[0];
      })
      .attr('y', function(d){
        return d[1];
      })
      .attr("transform", function(d){
        return 'rotate(-30 ' + d[0] + ' ' + d[1] + ')'
      })
      .text(function(d,i){
          console.log(stations[i]);
          return stations[i]["name"];
      })
      .style("font-size", "6px")
      .style("fill", "white")
      .style("opacity", "0.5");

}

function calcPolygonArea(polygon) {
  let N = polygon.length;
  let polygon_area = 0;
  polygon.forEach(function(d, i){
    if (i!==N-1) {
      polygon_area += d[0] * polygon[i+1][1] - polygon[1+i][0] * d[1];
    } else {
      polygon_area += d[0] * polygon[0][1] - polygon[0][0] * d[1];
    }
  });
  return Math.abs(polygon_area * 0.5);
}

function getTargetStationFromID (id){
  const target_array = (parseInt(id) > city_length) ? stations_2 : stations;
  let ret_object = {}
  target_array.forEach(function(d){
    if (parseInt(d["id"]) === parseInt(id)) ret_object = d;
  });
  return ret_object;
}

function plotCoordinates(projection, filename, id, color) {
  $.get("./" + filename, function(coordinates_raw){
    let projected_coordinate = [];
    let coordinates =  $.parseJSON(coordinates_raw);
    console.log(coordinates);

    let total_distance = 0;
    console.log(id);
    let target_station = getTargetStationFromID(id);
    console.log(target_station);

    const centre_of_tokyo = {"name": "Tokyo", "lng": 139.7649361, "lat": 35.6812362};
    let distance_from_tokyo = Math.sqrt( Math.pow(centre_of_tokyo["lng"]-target_station["lng"], 2) + Math.pow(centre_of_tokyo["lat"]-target_station["lat"], 2) );

    coordinates.forEach(function(d){
      d["city_id"] = id;
      total_distance += Math.sqrt( Math.pow(d["lng"]-target_station["lng"], 2) + Math.pow(d["lat"]-target_station["lat"], 2) );
      projected_coordinate.push(projection([d["lng"], d["lat"]]));
    });

    let circles_g = d3.select("#plot").append('g')
            .attr('class', 'estate_circles_g')
            .attr('id', 'circles_' + id);

    let hull_g = d3.select("#hull").append('g')
            .attr('class', 'estate_hull_g')
            .attr('id', 'hulls_' + id);

    let polygon = d3.polygonHull(projected_coordinate.map(function(d){
        return [d[0], d[1]];
    }));

    let polygon_area = calcPolygonArea(polygon);
    let polygon_centroid = d3.polygonCentroid(polygon);

    const kilometer_trans = 1/0.0090133729745762;
    console.log(coordinates[0]["name"]);
    console.log(projected_coordinate.length, polygon_area);
    console.log("total_distance", total_distance);
    console.log("average_distance", (total_distance/projected_coordinate.length) * kilometer_trans);
    console.log("distance_from_tokyo", distance_from_tokyo * kilometer_trans);

    let hull = hull_g.append("path");

    hull.datum(polygon)
        .attr("d", function(d) { return "M" + d.join("L") + "Z"; })
        .attr("fill", function(d){
            return color;
        })
        .attr("stroke", function(d){
            return color;
        })
        .attr("opacity", "0.2")
        .attr("id", function(d){
            return id + "_hull";
        });

    let contourDensity = d3.contourDensity()
      .x(function(d) { return d[0]; })
      .y(function(d) { return d[1]; })
      .size([width, height])
      .cellSize(5)
      .bandwidth(5)

    let contourDensityValues = contourDensity(projected_coordinate);

    const contour_color = d3.scaleSequential(function(t) { return d3.interpolate(color, "white")(1-t); })
      .domain([d3.max(contourDensityValues, function(d) { return d.value }), 0.00]);

    // overlap contour on convex hull
    d3.select("#hull").append("g")
      .attr("stroke", "none")
      .attr("stroke-width", "0.0")
      .selectAll("path")
      .data(contourDensityValues)
      .enter()
      .append("path")
      .attr("d", d3.geoPath())
      .attr("stroke", "none")
      // .attr("stroke-width", function(d) { return contour_color(d.value);})
      .attr("fill", function(d) { return contour_color(d.value);})
      .attr("opacity", function(d){
        // polygon外のcontourを非表示にする
        let flag = true;

        d.coordinates.forEach(function(coordinate){
          coordinate[0].forEach(function(c){
            if(!d3.polygonContains(polygon, c)) flag = false;
          });
        });

        return (flag)? "0.05": "0.0";
      });

    let circles = circles_g.selectAll("circle")
        .data(projected_coordinate)
        .enter()
        .append('circle')
        .attr('class', 'estate_circle')
        .attr('cx', function(d){
          return d[0];
        })
        .attr('cy', function(d){
          return d[1];
        })
        .attr('r', 0.5)
        .attr('stroke', color)
        .attr('fill', color)
        .style('opacity', function(d,i){
          return 0.5;
        })
        .on('mouseover', function(d,i){
          d3.select("#tooltip")
            .style("visibility", "visible")
            .style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px")
            .text(coordinates[i]["name"])
            .style("color", "aquamarine")
            .style("background-color", "dimgray");

          d3.select("#city_name").html(target_station["name"]);
          d3.select("#estate_num").html("Num: " + projected_coordinate.length);
          d3.select("#estate_sparse").html("Estate Sparse: " +(polygon_area/projected_coordinate.length).toFixed(2));
          d3.select("#average_distance").html("Average Distance: " + (total_distance/projected_coordinate.length * kilometer_trans).toFixed(2) + "[km]");
          d3.select("#distance_from_tokyo").html("From Tokyo: " + (distance_from_tokyo * kilometer_trans).toFixed(2) + "[km]");
        });
  });

}
