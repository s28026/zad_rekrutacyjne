function timeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sleep(fn, ...args) {
  await timeout(500);
  return fn(...args);
}

async function get_task_result(task_id) {
  const response = await fetch(`/task/check/${task_id}`, {
    method: "GET",
  });

  const data = await response.json();

  console.log(data);
  if (data.status === "SUCCESS") {
    console.log("Task result:", data.result);
    return data;
  } else if (data.status === "FAILED" || data.status == "FAILURE") {
    console.error("Task failed:", data.error);
  } else {
    console.log("Task status:", data.status);
    return await sleep(get_task_result, task_id);
  }
}

function apply_error(className, error) {
  document.querySelector(className).style.display = "inline-block";
  document.querySelector(className).innerHTML = error;
  document.querySelector(className).classList.add("alert");
}
