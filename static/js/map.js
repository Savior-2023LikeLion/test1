window.initMap = function () {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.5400456, lng: 126.9921017 },
    zoom: 5,
  });

  const infowindow = new google.maps.InfoWindow();

  const searchButton = document.getElementById("search-button");

  searchButton.addEventListener("click", function () {
    const input = document.getElementById("pac-input");
    const query = input.value;
    searchPlaces(query);
  });

  function searchPlaces(query) {
    const placesService = new google.maps.places.PlacesService(map);

    placesService.textSearch({ query: query }, function (results, status) {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        const bounds = new google.maps.LatLngBounds();

        results.forEach(function (place) {
          if (place.geometry.viewport) {
            bounds.union(place.geometry.viewport);
          } else {
            bounds.extend(place.geometry.location);
          }
        });

        map.fitBounds(bounds);
      } else {
        console.log("Place search failed with status:", status);
      }
    });
  }

  var searchBox = new google.maps.places.SearchBox(document.getElementById("pac-input"));

  google.maps.event.addListener(searchBox, "places_changed", function () {
    var places = searchBox.getPlaces();
    var bounds = new google.maps.LatLngBounds();

    places.forEach(function (place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      if (place.geometry.viewport) {
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });

    map.fitBounds(bounds);
  });

  const malls = [
    {
      label: "",
      name: "일본, 도쿄",
      lat: 35.5042949,
      lng: 138.4503955,
      pageUrl: japanPageUrl,
    },
    {
      label: "",
      name: "베트남, 하노이",
      lat: 21.022802,
      lng: 105.7590216,
      pageUrl: vietnamPageUrl,
    },
    {
      label: "",
      name: "미국, 워싱턴DC",
      lat: 38.8939059,
      lng: -77.1793867,
      pageUrl: USAPageUrl,
    },
  ];

  malls.forEach(({ label, name, lat, lng, pageUrl }) => {
    const marker = new google.maps.Marker({
      position: { lat, lng },
      label,
      map,
    });

    marker.addListener("click", () => {
      window.location.href = pageUrl;
      map.panTo(marker.position);
      infowindow.setContent(name);
      infowindow.open({
        anchor: marker,
        map,
      });
    });
  });
};
