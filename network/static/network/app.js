console.log("okay");

document.querySelector("#tweet-form").onsubmit = () => {
  console.log("!");
  const content = document.querySelector("#tweet-content").value;
  console.log(content);
  fetch("create", {
    method: "POST",
    body: JSON.stringify({
      content: content,
    }),
  })
    .then(() => {
      console.log("sucessfully posted ");
      document.querySelector("#tweet-form").reset;
      window.onload();
    })
    .catch((error) => console.log("error:", error));
  return false;
};
