const toggle = document.getElementById("toggle");
const frog = document.getElementById("frog");
const sliderText = document.getElementById("slider-text");
const sideText = document.querySelector(".my-side-dsc");

toggle.addEventListener("change", () => {

    // 점프 이미지
    frog.src = frog.dataset.jump;

    setTimeout(() => {

        if (toggle.checked) {
        frog.style.left = "140px"; // B 위치
    } else {
        frog.style.left = "25px";  // A 위치
    }

    document.querySelector(".my-side-dsc").innerText =
        toggle.checked ? "당신은 B SIDE!" : "당신은 A SIDE!";


    }, 150);

    // 착지 이미지
    setTimeout(() => {
        frog.src =  frog.dataset.land;
    }, 350);

    // 다시 앉은 상태
    setTimeout(() => {
        frog.src = frog.dataset.sit;
    }, 600);

});