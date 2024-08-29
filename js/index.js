document.addEventListener("DOMContentLoaded", function(){
  emojisData();
  addMessage();
  tiempoData();
  showTiempo();
});

function emojisData() {

  document.getElementById('textInput').addEventListener('input', function() {
    clearTimeout(timeout); 

    timeout = setTimeout(() => {
      traducirEmojis(this.value);
    }, 500); 
  });
}
  
async function traducirEmojis(texto) {
  const iconsWrap = document.getElementById('iconsWrap'); 

  if (texto.trim() === "") {
    iconsWrap.innerHTML = "";
    iconsWrap.classList.remove("show");
    return;
  }else{
    iconsWrap.classList.add("show");
  }

  try {
    let respuesta = await fetch(`${URL_PYTHON}/emojis?texto=${encodeURIComponent(texto)}`);
    respuesta = await respuesta.json();

    const emojisSet = new Set(respuesta.flatMap(
      item => [...item.emojis.trim()]
    ));

    iconsWrap.innerHTML = Array.from(emojisSet).map(
      emoji => `<span class="icon">${emoji}</span>`
    ).join('');
    inputIcon();

  } catch (error) {
    console.error("Error al traducir a emojis:", error);
    iconsWrap.innerHTML = "<span class='text-warning'>Error al traducir el texto</span>";
  }
}

function inputIcon(){
  var icon = document.querySelectorAll(".icon");
  var textInput = document.getElementById('textInput');

  icon.forEach((icon) => {
    if(icon){
      icon.onclick = () => {
        textInput.value += icon.textContent;
      }
    }
  })
}

function addMessage(){
  var submit = document.getElementById("submit");
  var blackBoard = document.getElementById("blackBoard");
  var iconsWrap = document.getElementById('iconsWrap'); 

  submit.onclick = (event) => {
    event.preventDefault();
    var valueInout = document.getElementById('textInput').value;

    if(valueInout != ""){
      var div = document.createElement("div");
      div.classList.add("messageWrap");
      div.classList.add("d-flex");
      div.classList.add("user");
  
      div.innerHTML = `
        <span class="eng" data-lang="ENG"></span>
        <span class="esp d-none" data-lang="ESP"></span>
        <p class="message">${valueInout}</p>
      `;
    
      blackBoard.append(div);
      blackBoard.scrollTop = blackBoard.scrollHeight;
  
      document.getElementById('textInput').value = " ";
      iconsWrap.classList.remove("show");

      div.querySelector(".eng").onclick = () => {
        setTimeout(function(){
          div.querySelector(".eng").classList.add("d-none");
          div.querySelector(".esp").classList.remove("d-none");
        },2000);
        var lang = div.querySelector(".eng").getAttribute("data-lang");
        traducirTexto(div, lang);
      }
      div.querySelector(".esp").onclick = () => {
        setTimeout(function(){
          div.querySelector(".eng").classList.remove("d-none");
          div.querySelector(".esp").classList.add("d-none");
        },2000);
        var lang = div.querySelector(".esp").getAttribute("data-lang");
        traducirTexto(div, lang);
      }

      setTimeout(() => {
        div.classList.add("show");
      }, 200);

      chat(valueInout);
      
    }
  }

}

async function obtenerTiempo(ciudad) {
  const respuesta = await fetch(`${URL_OPEN_WEATHER}&q=${ciudad}`);
  const datos = await respuesta.json(); 

  document.getElementById("tiempo").innerHTML = `
    <img src="https://openweathermap.org/img/wn/${datos.weather[0].icon}@4x.png">
  `;

  document.getElementById("tiempoData").innerHTML = `
    <h4 >${datos.weather[0].description}</h4>
    <p >Temperatura Actual: ${datos.main.temp} °C</p>
    <p >Temperatura Máxima: ${datos.main.temp_max} °C</p>
    <p >Temperatura Mínima: ${datos.main.temp_min} °C</p>
    <p >Humedad: ${datos.main.humidity} %</p>
    <p >Viento: ${datos.wind.speed} m/s</p>
    <p >Presión: ${datos.main.pressure} hPa</p>
   `;
}

async function obtenerEstadisticas(ciudad) {
  let datos = await fetch(`${URL_PYTHON}/tiempo?ciudad=${ciudad}`);
  datos = await datos.json(); 

  document.getElementById('tiempoData2').innerHTML = `
    <h5 >Promedio</h5>
    <p >Media de temperatura: ${datos.media_temperatura.toFixed(2)} °C</p>
    <p >Temperatura máxima: ${datos.max_temperatura} °C</p>
    <p >Temperatura mínima: ${datos.min_temperatura} °C</p>
    <p >Media de humedad: ${datos.media_humedad} %</p>
    <p >Media de viento: ${datos.media_viento.toFixed(2)} m/s</p>
    <p >Media de presión: ${datos.media_presion} hPa</p>
  `;
}

function obtenerGrafica(ciudad) {
  document.getElementById('graficaTiempo').innerHTML = `
    <img src="${URL_PYTHON}/tiempo/grafica?ciudad=${ciudad}" class="img-fluid mt-4">
  `;
}

async function tiempoData() {
  const ciudad = document.getElementById("ciudad"); 
  ciudad.value = "Elche";

  document.getElementById('ciudad').addEventListener('input', function() {
    clearTimeout(timeout); 

    timeout = setTimeout(() => {
      obtenerTiempo(ciudad.value);
      obtenerEstadisticas(ciudad.value);
      obtenerGrafica(ciudad.value);
    }, 500); 

  });


  await obtenerTiempo(ciudad.value);
  await obtenerGrafica(ciudad.value);
  await obtenerEstadisticas(ciudad.value);
}

function showTiempo(){
  var button = document.getElementById("tiempo");
  var tiempoInfo = document.getElementById("tiempoInfo");
  var closeTiempo = document.getElementById("closeTiempo");

  button.onclick = (event) => {
    event.preventDefault();
    tiempoInfo.classList.add("showTiempo");
    
  }

  closeTiempo.onclick = (event) => {
    event.preventDefault();
    tiempoInfo.classList.remove("showTiempo");
  }

}

async function traducirTexto(div, lang) {
  var texto = div.querySelector(".message").textContent;

  try {
    let respuesta = await fetch(`${URL_PYTHON}/traductor?texto=${encodeURIComponent(texto)}&lang=${lang}`);
    respuesta = await respuesta.json(); 

    div.querySelector(".message").textContent = respuesta.traduccion; 
  } catch (error) {
    console.error("Error al traducir el texto:", error);
    div.innerHTML = "<span class='text-warning'>Error al traducir el texto</span>";
  }
}

async function chat(texto){
  try {
    console.log(`${URL_PYTHON}/chat?texto=${encodeURIComponent(texto)}`);
    let respuesta = await fetch(`${URL_PYTHON}/chat?texto=${encodeURIComponent(texto)}`);
    respuesta = await respuesta.json(); 

    var div = document.createElement("div");
    div.classList.add("messageWrap");
    div.classList.add("d-flex");
    div.classList.add("chat");

    div.innerHTML = `
      <span class="eng" data-lang="ENG"></span>
      <span class="esp d-none" data-lang="ESP"></span>
      <p class="message">${respuesta.respuesta}</p>
    `;
  
    blackBoard.append(div);
    blackBoard.scrollTop = blackBoard.scrollHeight;

    document.getElementById('textInput').value = " ";
    iconsWrap.classList.remove("show");

    div.querySelector(".eng").onclick = () => {
      setTimeout(function(){
        div.querySelector(".eng").classList.add("d-none");
        div.querySelector(".esp").classList.remove("d-none");
      },2000);
      var lang = div.querySelector(".eng").getAttribute("data-lang");
      traducirTexto(div, lang);
    }
    div.querySelector(".esp").onclick = () => {
      setTimeout(function(){
        div.querySelector(".eng").classList.remove("d-none");
        div.querySelector(".esp").classList.add("d-none");
      },2000);
      var lang = div.querySelector(".esp").getAttribute("data-lang");
      traducirTexto(div, lang);
    }

    setTimeout(() => {
      div.classList.add("show");
    }, 200);

  } catch (error) {
    console.error("Error al traducir el texto:", error);
    div.innerHTML = "<span class='text-warning'>Error al traducir el texto</span>";
  }
}