print "Hello, world!";
var a = 1; var b = 3; var c = 5; print a + b + c;
fun printSum(a, b) {
  print a + b;
}

printSum(10, 15);
fun getSum(a, b) {
  return a + b;
}

var sum = getSum(4, 5);

if(sum > 10) {
print "yes";
} else if(sum > 20) {
print "maybe";
} else {
print "no";
}

fun a1(a) { return a*2; }
fun a2(b) { return a/2; }

print a1(4) * a2(10); print a2(5) / a1(50);



var c = nil;

if(a1(4) > 5) { print "ok"; }
c = 40; print c;