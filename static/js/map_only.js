window.initMap = function () {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.5400456, lng: 126.9921017 },
    zoom: 5,
  });

  const infowindow = new google.maps.InfoWindow();

  const malls = [
    { label: "", name: "일본, 도쿄", lat: 35.5042949, lng: 138.4503955 },
    { label: "", name: "베트남, 하노이", lat: 21.022802, lng: 105.7590216 },
    { label: "", name: "미국, 워싱턴DC", lat: 38.8939059, lng: -77.1793867 },
  ];
  malls.forEach(({ label, name, lat, lng }) => {
    const marker = new google.maps.Marker({
      position: { lat, lng },
      label,
      map,
    });

    marker.addListener("click", () => {
      map.panTo(marker.position);
      infowindow.setContent(name);
      infowindow.open({
        anchor: marker,
        map,
      });
    });
  });
};
