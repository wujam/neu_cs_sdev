# 13
## Files
- xserver: systems level test harness for Santorini
- xclient: systems level test harness for Santorini
- client-tests: contains sample input to use with xclient
  - X-in.json (X between 1 and 1 inclusive)
- server-tests: contains sample input and outputs to use with xserver
  - X-in.json (X between 1 and 1 inclusive)
  - X-out.json (X between 1 and 1 inclusive)

## Running Systems Test Harnesses
xserver can run the server component with "cat server-tests/X-in.json | xserver" 
xclient can run the client player components in different processes with "cat client-tests/X-in.json | xclient" 
