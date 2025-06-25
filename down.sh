mrg xdc detach x0.$USER || true
mrg demat test.gate.$USER || true
mrg relinquish test.gate.$USER || true
mrg delete xdc x0.$USER || true
mrg delete experiment gate.$USER || true