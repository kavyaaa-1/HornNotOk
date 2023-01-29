<?php
$username = $_POST['username'];
$email = $_POST['email'];
$password = $_POST['password'];
$age = $_POST['age'];
$medical = $_POST['medical_condition']

if(!empty($username) || !empty($email) || !empty($password) || !empty($age) || !empty($medical)){

    $host = "localhost";
    $dbUsername = "root";
    $dbPassword = "No";
    $dbname = "hornnotokay"

    $conn = new mysqli($host, $dbUsername, $dbPassword, $dbname);

    if(mysqli_connect_error()){
        die('Connect Error('.mysqli_connect_errno)
    }
    else{
        $SELECT = "SELECT email FROM "user info" WHERE email = ? LIMIT 1";
        $INSERT = "INSERT INTO "user info" (username, password, email, age, medical) VALUES(?,?,?,?,?)";

        $stmt = $conn->prepare($Select);
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $stmt->bind_result($resultEmail);
        $stmt->store_result();
        $stmt->fetch();
        $rnum = $stmt->num_rows;
        if ($rnum == 0) {
            $stmt->close();
            $stmt = $conn->prepare($Insert);
            $stmt->bind_param("sssis",$username, $password, $email, $age, $medical);
            if ($stmt->execute()) {
                echo "New record inserted sucessfully.";
            }
            else {
                echo $stmt->error;
            }
        }
        else {
            echo "Someone already registers using this email.";
        }
        $stmt->close();
        $conn->close();
        }

}
else{
    echo "All fields are required";
    die();
}

?>