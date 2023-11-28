
function like(postId) {
  let thumb = document.getElementById(`like-button-${postId}`);
  let likeCounter = document.getElementById(`like-post-${postId}`);

  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      // console.log(data);
      // console.log(thumb);
      likeCounter.innerHTML = data["likes"];
      if (data["liked"]) {
        thumb.classList.toggle("fas");
        thumb.classList.remove("sel-far");
      } else {
        thumb.classList.toggle("far");
        thumb.classList.add("sel-far");
      }
    })
    .catch((e) => alert("Couldn't like this post. Be sure to log in frist."));
}
